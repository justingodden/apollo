import { useState, useContext } from 'react'
import { WatchContext } from '../context/WatchContext'
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';


const minYear = 1980
const maxYear = 2022
const years = []
for (let i = maxYear; i >= minYear; i--) years.push(i)
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
}


export default function YearSelect() {
    const [year, setYear] = useState('')
    const [watch, setWatch] = useContext(WatchContext)

    const handleChange = (e) => {
        let tempWatch = watch
        setYear(e.target.value)
        tempWatch.year = e.target.value
        setWatch(tempWatch)
    }

    return (
        <Box sx={{ minWidth: 120 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Year</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={year}
                    label="Year"
                    onChange={handleChange}
                    MenuProps={MenuProps}
                >{
                        years.map(year => <MenuItem key={year} value={year}>{year}</MenuItem>)
                    }
                </Select>
            </FormControl>
        </Box>
    );
}