import '@/styles/global.css'
import { Provider } from 'react-redux'
import store from './redux/store'
import HCPInteractionPage from './pages/HCPInteractionPage'

export default function App() {
  return (
    <Provider store={store}>
      <HCPInteractionPage />
    </Provider>
  )
}
