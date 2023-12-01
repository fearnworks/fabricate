// test-utils.ts
import { render } from '@testing-library/vue'

export function renderWithProps(component: any, props: any) {
  const showToast = () => {}
  return render(component, {
    props,
    global: {
      provide: {
        showToast
      }
    }
  })
}