import AppStore from '../store/app'

export const error = (error: string) => {
  console.error(error)
  AppStore.mutations.SET_ERROR(AppStore.state, error)
  setTimeout(() => {
    AppStore.mutations.SET_ERROR(AppStore.state, null)
  }, 5000)
}