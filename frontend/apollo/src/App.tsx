import { useState, useContext } from 'react'
import './App.css'
import { WatchContext } from './context/WatchContext'
import BrandSeriesSelect from './components/BrandSeriesSelect'
import YearSelect from './components/YearSelect'
import Checkboxes from './components/Checkboxes'
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';

function App() {
  const [loading, setLoading] = useState(false)
  const [price, setPrice] = useState('')
  const [watch, setWatch] = useContext(WatchContext)

  async function handleClick() {
    setLoading(true)
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(watch)
    })
    const content = await response.json()
    setPrice(content)
    setLoading(false)
  }

  return (
    <div className="App">
      <div className="App-background">
        <div className="Main-container">
          <h3>Value your watch!</h3>
          {
            loading ? <CircularProgress style={{ marginTop: '20px' }} /> : `Watch Price: £${price}`
          }
          <BrandSeriesSelect />
          <YearSelect />
          <Checkboxes />
          <Button
            onClick={() => handleClick()}
            variant="contained">get watch price</Button>

        </div>
      </div>
    </div>
  )
}

export default App
