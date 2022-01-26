import { useState, createContext } from 'react'


export const WatchContext = createContext()

export const WatchProvider = props => {
    const [watch, setWatch] = useState(
        {
            brand: null,
            series: null,
            year: null,
            box: false,
            papers: false
        }
    )
    return (
        <WatchContext.Provider value={[watch, setWatch]}>
            {props.children}
        </WatchContext.Provider>
    )
}