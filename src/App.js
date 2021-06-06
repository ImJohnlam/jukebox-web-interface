import React, { useState, useEffect, useContext } from 'react';
import { Button } from 'react-bootstrap';
import './App.css';
import { SampleSelect, FilterSelect, Result } from './components/components'

function App() {
   const [currentTime, setCurrentTime] = useState(0);

   // Test api call
   useEffect(() => {
      fetch('/time').then(res => res.json()).then(data => setCurrentTime(data.time));
   }, []);

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
         <Result/>
         <p>The current time is {currentTime}.</p>
    </section>
  );
}

export default App;
