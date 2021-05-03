import React, { useState, createContext } from 'react'

const GenerateContext = createContext();
const GenerateContextProvider = props => {
   const [sample, setSample] = useState('');
   const [filters, setFilters] = useState([]);

   const getGenState = type => {
      switch (type) {
         case 'SAMPLE':
            return sample;
         case 'FILTERS':
            return filters;
         default:
            throw Error();
      }
   }

   const setGenState = (type, state) => {
      switch (type) {
         case 'SAMPLE':
            setSample(state);
            break;
         case 'FILTERS':
            setFilters(state);
            break;
         default:
            throw Error();
      }
   }

   return (
      <GenerateContext.Provider value={[getGenState, setGenState]}>
         {props.children}
      </GenerateContext.Provider>
   );
}

export { GenerateContext, GenerateContextProvider };