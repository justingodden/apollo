import { useContext } from 'react'
import { WatchContext } from '../context/WatchContext'
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

export default function Checkboxes() {
    const [watch, setWatch] = useContext(WatchContext)

    const handlePapers = (e) => {
        let tempWatch = watch
        tempWatch.papers = e.target.checked
        setWatch(tempWatch)
    }

    const handleBox = (e) => {
        let tempWatch = watch
        tempWatch.box = e.target.checked
        setWatch(tempWatch)
    }

    return (
        < FormGroup className="Form-group" >
            <FormControlLabel control={<Checkbox onChange={handleBox} />} label="Box" />
            <FormControlLabel control={<Checkbox onChange={handlePapers} />} label="Papers" />
        </FormGroup >
    )
}