import * as React from 'react'

const TOAST_LIMIT = 4
const listeners = []
let memoryState = { toasts: [] }
let count = 0

function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER
  return count.toString()
}

function dispatch(action) {
  memoryState = reducer(memoryState, action)
  listeners.forEach((listener) => listener(memoryState))
}

function reducer(state, action) {
  switch (action.type) {
    case 'ADD_TOAST':
      return { ...state, toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT) }
    case 'DISMISS_TOAST':
      return {
        ...state,
        toasts: state.toasts.map((t) => (t.id === action.toastId || !action.toastId ? { ...t, open: false } : t)),
      }
    case 'REMOVE_TOAST':
      if (!action.toastId) return { ...state, toasts: [] }
      return { ...state, toasts: state.toasts.filter((t) => t.id !== action.toastId) }
    default:
      return state
  }
}

function toast({ ...props }) {
  const id = genId()
  const update = (props) => dispatch({ type: 'ADD_TOAST', toast: { ...props, id } })
  const dismiss = () => dispatch({ type: 'DISMISS_TOAST', toastId: id })

  dispatch({
    type: 'ADD_TOAST',
    toast: { ...props, id, open: true, onOpenChange: (open) => !open && dismiss() },
  })

  setTimeout(() => dismiss(), props.duration || 4000)

  return { id, update, dismiss }
}

function useToast() {
  const [state, setState] = React.useState(memoryState)

  React.useEffect(() => {
    listeners.push(setState)
    return () => {
      const idx = listeners.indexOf(setState)
      if (idx > -1) listeners.splice(idx, 1)
    }
  }, [])

  return { ...state, toast, dismiss: (id) => dispatch({ type: 'DISMISS_TOAST', toastId: id }) }
}

export { useToast, toast }
