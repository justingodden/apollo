import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'
import { WatchProvider } from './context/WatchContext';

ReactDOM.render(
  <React.StrictMode>
    <WatchProvider>
      <App />
    </WatchProvider>
  </React.StrictMode>,
  document.getElementById('root')
)
