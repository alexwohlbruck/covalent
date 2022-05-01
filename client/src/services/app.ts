import AppStore from '../store/app'

export const showError = (message: string) => {
  console.error(message)
  AppStore.mutations.SET_ERROR(AppStore.state, message)
  setTimeout(() => {
    AppStore.mutations.SET_ERROR(AppStore.state, null)
  }, 5000)
}