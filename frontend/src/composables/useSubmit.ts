import { ref } from 'vue'

import { ApiError } from '../api'

export type SubmitState = 'idle' | 'sending' | 'ok' | 'error'

/** Tracks one form's submit: a state for the button and a message for the status line. */
export function useSubmit(send: () => Promise<unknown>, okMessage: string) {
  const state = ref<SubmitState>('idle')
  const message = ref('')

  async function submit(): Promise<boolean> {
    if (state.value === 'sending') return false
    state.value = 'sending'
    message.value = ''
    try {
      await send()
      state.value = 'ok'
      message.value = okMessage
      return true
    } catch (e) {
      state.value = 'error'
      message.value = e instanceof ApiError ? e.message : 'Something went wrong. Try again.'
      return false
    }
  }

  return { state, message, submit }
}
