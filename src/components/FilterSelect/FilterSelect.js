import React, { useEffect, useState, useContext } from 'react';
import { Button } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext';

const FilterObj = (props) => {
   const [getGenState, setGenState] = useContext(GenerateContext);
   const initialParamState = props.params.reduce((acc, param) => {
      let {name, value} = param;
      return {...acc, [name]:value};
   }, {});
   const [paramState, setParamState] = useState(initialParamState);
   const handleChange = ev => setParamState({...paramState, [ev.target.name]: ev.target.value})

   const isSelected = () => getGenState('FILTERS').find(f => f.name === props.name);
   const select = () => setGenState('FILTERS', getGenState('FILTERS').concat({name: props.name, params:{...paramState}}));
   const cancel = () => setGenState('FILTERS', getGenState('FILTERS').filter(f => f.name !== props.name));

   return (
      <div>
         <h3>{props.name}</h3>
         {props.params.map((param, idx) =>
            <div key={idx}>
               {param.name}
               <input name={param.name}
                      type="range" min={param.min}
                      max={param.max}
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
      </div>
   );
}

export default function FilterSelect(props) {
   return (
      <section className='container'>
         <h2>Apply filters</h2>
         <FilterObj name="example filter1"
                    params={[{
                       name: "example param1",
                       min: 1,
                       max: 100,
                       value: 50
                     },{
                       name: "example param2",
                       min: 20,
                       max: 20000,
                       value: 5000
                     }
                  ]
         }/>
         <FilterObj name="example filter2"
                    params={[{
                       name: "example param3",
                       min: 50,
                       max: 5000,
                       value: 2500
                     }
                  ]
         }/>
      
         
      </section>
   );
}