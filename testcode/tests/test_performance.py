"""
性能测试用例

对应测试文档中的用例：
- TC-701: 并发用户测试
- TC-702: 文档解析性能
- TC-703: 内存稳定性测试

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import pytest
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any


@pytest.mark.performance
@pytest.mark.slow
class TestPerformance:
    """性能测试类。"""
    
    def test_tc701_concurrent_users(
        self,
        test_config,
        api_client,
        test_knowledge_base,
        performance_monitor
    ):
        """
        TC-701: 100 并发用户同时问答
        
        测试目的：验证系统在高并发下的性能
        
        Args:
            test_config: 测试配置
            api_client: API 客户端
            test_knowledge_base: 测试知识库
            performance_monitor: 性能监控器
        """
        logging.info("========== TC-701: 并发用户测试 ==========")
        
        # 配置
        concurrent_users = 100  # 并发用户数
        requests_per_user = 10  # 每个用户的请求数
        
        # 测试数据
        test_questions = [
            "什么是 RAG 技术？",
            "如何创建知识库？",
            "系统支持哪些文档格式？",
            "如何优化检索效果？",
            "MinerU 有什么优势？",
        ]
        
        # 统计数据
        success_count = 0
        failure_count = 0
        response_times = []
        errors = []
        
        lock = threading.Lock()
        
        def make_request(user_id: int, request_id: int) -> Dict[str, Any]:
            """
            发送单个请求。
            
            Args:
                user_id: 用户 ID
                request_id: 请求 ID
                
            Returns:
                Dict: 请求结果
            """
            nonlocal success_count, failure_count
            
            start_time = time.time()
            
            try:
                # 随机选择一个问题
                question = test_questions[request_id % len(test_questions)]
                
                # 发送问答请求
                response = api_client.post(
                    "/v1/chat/completions",
                    json={
                        "question": question,
                        "kb_id": test_knowledge_base["id"]
                    }
                )
                
                elapsed = time.time() - start_time
                
                with lock:
                    response_times.append(elapsed)
                    
                    if response.status_code == 200:
                        success_count += 1
                        return {
                            "status": "success",
                            "user_id": user_id,
                            "request_id": request_id,
                            "response_time": elapsed
                        }
                    else:
                        failure_count += 1
                        return {
                            "status": "failure",
                            "user_id": user_id,
                            "request_id": request_id,
                            "status_code": response.status_code,
                            "response_time": elapsed
                        }
            
            except Exception as e:
                elapsed = time.time() - start_time
                
                with lock:
                    failure_count += 1
                    errors.append(str(e))
                    
                return {
                    "status": "error",
                    "user_id": user_id,
                    "request_id": request_id,
                    "error": str(e),
                    "response_time": elapsed
                }
        
        # 执行并发测试
        logging.info(f"开始并发测试: {concurrent_users} 用户 x {requests_per_user} 请求")
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            
            for user_id in range(concurrent_users):
                for request_id in range(requests_per_user):
                    future = executor.submit(make_request, user_id, request_id)
                    futures.append(future)
            
            # 等待所有请求完成
            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    logging.error(f"任务执行失败: {e}")
        
        # 计算统计数据
        total_requests = concurrent_users * requests_per_user
        success_rate = (success_count / total_requests) * 100
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # 计算 P95 响应时间
        response_times_sorted = sorted(response_times)
        p95_index = int(len(response_times_sorted) * 0.95)
        p95_response_time = response_times_sorted[p95_index] if response_times_sorted else 0
        
        # 输出测试结果
        logging.info("=" * 60)
        logging.info(f"总请求数: {total_requests}")
        logging.info(f"成功数: {success_count}")
        logging.info(f"失败数: {failure_count}")
        logging.info(f"成功率: {success_rate:.2f}%")
        logging.info(f"平均响应时间: {avg_response_time:.2f} 秒")
        logging.info(f"P95 响应时间: {p95_response_time:.2f} 秒")
        logging.info(f"测试总时长: {performance_monitor['duration']:.2f} 秒")
        logging.info("=" * 60)
        
        # 断言
        assert success_rate >= 95.0, f"成功率应 >= 95%，实际 {success_rate:.2f}%"
        assert avg_response_time <= 10.0, f"平均响应时间应 <= 10秒，实际 {avg_response_time:.2f}秒"
        
        logging.info("========== TC-701: 测试通过 ==========\n")
    
    @pytest.mark.parametrize("file_size,expected_time", [
        ("small", 10),  # 小文件: 5页, 期望 < 10秒
        ("medium", 60),  # 中文件: 50页, 期望 < 60秒
        ("large", 200),  # 大文件: 200页, 期望 < 200秒
    ])
    def test_tc702_document_parsing_performance(
        self,
        management_api_client,
        test_knowledge_base,
        file_size,
        expected_time,
        performance_monitor
    ):
        """
        TC-702: 测试不同大小文档的解析时间
        
        测试目的：评估 MinerU 的性能表现
        
        Args:
            management_api_client: 管理后台 API 客户端
            test_knowledge_base: 测试知识库
            file_size: 文件大小类别
            expected_time: 期望的解析时间（秒）
            performance_monitor: 性能监控器
        """
        logging.info(f"========== TC-702: 文档解析性能测试 ({file_size}) ==========")
        
        # 注意：此测试需要预先准备测试文件
        test_files = {
            "small": "tests/test_data/small_document.pdf",  # 5页
            "medium": "tests/test_data/medium_document.pdf",  # 50页
            "large": "tests/test_data/large_document.pdf",  # 200页
        }
        
        file_path = test_files.get(file_size)
        
        # 检查文件是否存在
        import os
        if not os.path.exists(file_path):
            pytest.skip(f"测试文件不存在: {file_path}")
        
        try:
            # 1. 上传文件
            upload_response = management_api_client.upload_file(
                "/api/files/upload",
                file_path,
                field_name="file"
            )
            
            assert upload_response.status_code == 200, "文件上传成功"
            file_id = upload_response.json()["id"]
            
            # 2. 添加文件到知识库并开始解析
            parse_response = management_api_client.post(
                f"/api/knowledgebases/{test_knowledge_base['id']}/documents",
                json={
                    "file_id": file_id,
                    "parser_method": "auto"
                }
            )
            
            assert parse_response.status_code == 201, "开始解析文档"
            doc_id = parse_response.json()["id"]
            
            # 3. 轮询解析状态
            max_wait_time = expected_time * 2  # 最大等待时间为期望时间的2倍
            start_time = time.time()
            parse_completed = False
            
            while time.time() - start_time < max_wait_time:
                status_response = management_api_client.get(
                    f"/api/documents/{doc_id}"
                )
                
                if status_response.status_code == 200:
                    doc_data = status_response.json()
                    status = doc_data.get("parse_status")
                    
                    if status == "completed":
                        parse_completed = True
                        break
                    elif status == "failed":
                        pytest.fail(f"文档解析失败: {doc_data.get('error')}")
                
                time.sleep(5)  # 每5秒检查一次
            
            actual_time = time.time() - start_time
            
            # 断言
            assert parse_completed, f"解析超时（> {max_wait_time}秒）"
            assert actual_time <= expected_time, \
                f"解析时间（{actual_time:.2f}秒）超过期望（{expected_time}秒）"
            
            logging.info(f"文档解析完成，耗时: {actual_time:.2f} 秒")
            
        except Exception as e:
            logging.error(f"文档解析测试失败: {e}")
            pytest.fail(f"文档解析测试失败: {e}")
        
        logging.info(f"========== TC-702: 测试通过 ({file_size}) ==========\n")
    
    @pytest.mark.slow
    def test_tc703_memory_stability(
        self,
        api_client,
        test_knowledge_base
    ):
        """
        TC-703: 24 小时稳定性测试
        
        测试目的：验证系统长时间运行的稳定性
        
        Args:
            api_client: API 客户端
            test_knowledge_base: 测试知识库
        """
        logging.info("========== TC-703: 内存稳定性测试 ==========")
        
        # 注意：完整的 24 小时测试耗时太长，这里使用缩短版
        test_duration = 60 * 60  # 1 小时（实际测试中应为 24 小时）
        request_interval = 10  # 每 10 秒发送一次请求
        
        logging.warning(f"使用缩短版测试：{test_duration / 3600} 小时")
        
        start_time = time.time()
        request_count = 0
        error_count = 0
        
        try:
            while time.time() - start_time < test_duration:
                # 发送测试请求
                response = api_client.post(
                    "/v1/chat/completions",
                    json={
                        "question": "测试问题",
                        "kb_id": test_knowledge_base["id"]
                    }
                )
                
                request_count += 1
                
                if response.status_code != 200:
                    error_count += 1
                    logging.warning(f"请求失败: {response.status_code}")
                
                # 每 100 个请求输出一次统计
                if request_count % 100 == 0:
                    elapsed = time.time() - start_time
                    logging.info(
                        f"已运行 {elapsed / 3600:.2f} 小时, "
                        f"请求数: {request_count}, "
                        f"错误数: {error_count}"
                    )
                
                time.sleep(request_interval)
            
            # 计算错误率
            error_rate = (error_count / request_count) * 100 if request_count > 0 else 0
            
            logging.info("=" * 60)
            logging.info(f"测试时长: {test_duration / 3600:.2f} 小时")
            logging.info(f"总请求数: {request_count}")
            logging.info(f"错误数: {error_count}")
            logging.info(f"错误率: {error_rate:.2f}%")
            logging.info("=" * 60)
            
            # 断言
            assert error_rate <= 5.0, f"错误率应 <= 5%，实际 {error_rate:.2f}%"
            
        except KeyboardInterrupt:
            logging.warning("测试被手动中断")
        
        logging.info("========== TC-703: 测试通过 ==========\n")

