import * as React from 'react';
import { Button as BaseButton } from '@base-ui/react/button';

export interface ButtonProps extends React.ComponentProps<typeof BaseButton> {
  className?: string;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => {
    return (
      <BaseButton
        ref={ref}
        className={className}
        {...props}
      />
    );
  }
);

Button.displayName = 'HeaderButton';

export { Button };
