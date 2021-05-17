import React, { useState, useEffect, useContext } from 'react';
import { Button } from 'react-bootstrap';
import './App.css';
import { GenerateContext, GenerateContextProvider } from './components/GenerateContext';
import { SampleSelect, FilterSelect, Result } from './components/components'
const axios = require('axios');

function App() {
   const [getGenState, _] = useContext(GenerateContext);
   const [currentTime, setCurrentTime] = useState(0);

   // Test api call
   useEffect(() => {
      fetch('/time').then(res => res.json()).then(data => setCurrentTime(data.time));
   }, []);

   const generate = async e => {
      const data = new FormData();

      e.preventDefault();
      data.append('file', getGenState('SAMPLE'))

      // TODO
      data.append('filters', JSON.stringify([{a: 123, b: '234'}]))

      console.log('uploading file:', getGenState('SAMPLE'))
      

      try {
         const response = await axios({
            method: 'post',
            url: 'http://localhost:5000/upload',
            data: data,
            responseType: 'blob'
         });
         console.log(response)
         const mp3 = new Blob([response.data], { type: 'audio/wav' })
         const url = window.URL.createObjectURL(mp3)
         const audio = new Audio(url)
         // audio.load()
         // DEBUG
         window.open(url, '_blank')
         // await audio.play()
       } catch (e) {
         console.log('play audio error: ', e)
       }
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
