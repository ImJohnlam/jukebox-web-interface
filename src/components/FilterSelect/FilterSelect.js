import React, { useEffect, useState, useContext } from 'react';
import { Button, CardImg, Card } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext';
import { getFilters } from '../../api';
import './FilterSelect.css'

const FilterObj = (props) => {
   const initialParamState = props.params.reduce((acc, param) => {
      let {name, value} = param;
      return {...acc, [name]:value};
   }, {});

   const [paramState, setParamState] = useState(initialParamState);
   const [getGenState, setGenState] = useContext(GenerateContext);

   const handleChange = ev => setParamState({...paramState, [ev.target.name]: ev.target.value})
   const select = () => setGenState('FILTERS', {name: props.name, params:{...paramState}});
   const isSelected = () => getGenState('FILTERS')['name'] == props.name
   const cancel = () => setGenState('FILTERS', {});

   return (
      <Card className='filter'>
         <h3>{props.name}</h3>
         {props.params.map((param, idx) =>
            <div key={idx}>
               {param.name}
               <input name={param.name}
                      type="range" min={param.lower_bound}
                      max={param.upper_bound}
                      value={paramState[param.name]}
                      disabled={isSelected()}
                      onChange={handleChange}/>
               {paramState[param.name]}
            </div>
         )}
         {isSelected() ?
         <Button onClick={cancel}>Cancel</Button>
         :
         <Button onClick={select}>Apply</Button>
         }
      </Card>
   );
}

export default function FilterSelect(props) {
   const [getGenState, setGenState] = useContext(GenerateContext);
   const [filters, setFilters] = useState([])

   useEffect(() => {
      getFilters().then(f => setFilters(f));
   }, []);

   return (
      <Card className='filter-selector'>
         <h2>Apply filters</h2>
         {filters && filters.length ? filters.map(filter => <FilterObj name={filter.name}
                                           params={filter.params}/>)
         : ""}
      </Card>
   );
}