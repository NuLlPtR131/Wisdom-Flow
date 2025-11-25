import { cva, type VariantProps } from 'class-variance-authority';
import * as React from 'react';

import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-all duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground hover:bg-primary/85 hover:shadow-sm',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/85 hover:shadow-sm',
        destructive:
          'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/85 hover:shadow-sm',
        outline: 'text-foreground hover:bg-muted/70',
        tertiary:
          'border-transparent bg-colors-background-core-strong text-colors-text-persist-light hover:bg-colors-background-core-strong/85 hover:shadow-sm',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
