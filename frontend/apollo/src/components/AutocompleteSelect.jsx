import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

export default function AutocompleteSelect({ options, label, onChange }) {
    return (
        <Autocomplete
            className="Input-box"
            disablePortal
            id="combo-box-demo"
            options={options}
            sx={{ width: 300 }}
            onChange={onChange}
            renderInput={(params) => <TextField {...params} label={label} />}
        />
    )
}