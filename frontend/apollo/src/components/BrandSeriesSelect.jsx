import { useState, useContext, useEffect } from 'react'
import { WatchContext } from '../context/WatchContext'
import AutocompleteSelect from "./AutocompleteSelect"

// let brandAndSeries = {
//     "Rolex": [
//         "Submariner",
//         "Daytona"
//     ],
//     "Omega": [
//         "Seamaster",
//         "Speedmaster"
//     ]
// }

// fetch('http://127.0.0.1:5000/brand-and-series.json')
//     .then(response => response.json())
//     .then(data => brandAndSeries = data)



export default function BrandSeriesSelect() {
    const [brands, setBrands] = useState([])
    const [series, setSeries] = useState([])
    const [apiData, setApiData] = useState({})
    const [seriesValue, setSeriesValue] = useState(null)
    const [watch, setWatch] = useContext(WatchContext)

    useEffect(() => {
        async function fetchData() {
            const response = await fetch('http://127.0.0.1:5000/brand-and-series.json')
            const data = await response.json()
            setApiData(data)
            setBrands(Object.keys(data))
        }
        fetchData()
    }, [])


    function handleBrandSelect(e, val) {
        setSeriesValue(null)
        setSeries(apiData[val])
        let tempWatch = watch
        tempWatch.brand = val
        setWatch(tempWatch)
    }

    function handleSeriesSelect(e, val) {
        let tempWatch = watch
        tempWatch.series = val
        setWatch(tempWatch)
    }

    return (
        <div>
            <AutocompleteSelect
                className="Input-box"
                options={brands}
                label="Brand"
                onChange={handleBrandSelect}
            />
            <AutocompleteSelect
                className="Input-box"
                options={series}
                label="Series"
                onChange={handleSeriesSelect}
                value={seriesValue}
            />
        </div>
    )
}


