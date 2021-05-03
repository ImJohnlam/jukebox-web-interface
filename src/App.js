import React, { useState, useEffect, useContext } from 'react';
import { Button } from 'react-bootstrap';
import './App.css';
import { GenerateContext, GenerateContextProvider } from './components/GenerateContext';
import { SampleSelect, FilterSelect, Result } from './components/components'

function App() {
   const [getGenState, _] = useContext(GenerateContext);
   const [currentTime, setCurrentTime] = useState(0);

   // Test api call
   useEffect(() => {
      fetch('/time').then(res => res.json()).then(data => setCurrentTime(data.time));
   }, []);

   const generate = () => {
      console.log(`generating a sample from ${getGenState('SAMPLE')}`)
      console.log('Filters:')
      getGenState('FILTERS').forEach(f => {
         console.log(f.name, f.params)
      })
      // TODO: real api call here
   }

   return (
      <section className='container'>
         <div>
            <h1>Welcome to Jukebox Web Interface</h1>
            <Button>Instructions</Button> 
            {/* TODO: instruction drop down */}
            <Button href="https://openai.com/blog/jukebox/">OpenAI Blog</Button>
         </div>
         <SampleSelect/>
         <FilterSelect/>
         <Button onClick={generate} disabled={getGenState('SAMPLE') === ""}>Generate</Button>
         <Result/>
         {/* TODO: results */}
         <p>The current time is {currentTime}.</p>
    </section>
  );
}

export default App;
