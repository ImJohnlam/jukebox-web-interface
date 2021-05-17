import React, { useEffect, useState, useContext } from 'react';
import { Button } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext';
const axios = require('axios');

const SampleObj = props => {
   const [getGenState, setGenState] = useContext(GenerateContext);

   const isSelected = () => getGenState('SAMPLE') == props.name;
   const select = () => setGenState('SAMPLE', props.name);

   return (
      <div>
         <b>{props.name} by {props.artist}</b>
         {isSelected() ?
         <Button disabled={true}>Selected</Button>
         :
         <Button onClick={select}>Select</Button>
         }
         <audio controls>
         <source src={props.src}/>
         </audio>
      </div>
   )
}

const UploadObj = props => {
   const [getGenState, setGenState] = useContext(GenerateContext);
   let uploadInput;

   const select = e  => {
      e.preventDefault();
      setGenState('SAMPLE', uploadInput.files[0]);
      console.log(`selected sample: ${getGenState('SAMPLE')}`);
   }

   return (
      <div>
            <b>Upload a .wav file</b>
            <form onSubmit={select}>
               <div>
                  <input ref={ref => uploadInput = ref} type="file"/>
               </div>
               <div>
                  <button>Select</button>
               </div>
            </form>
         </div>
   )
}

export default function SampleSelect(props) {
   return (
      <section className='container'>
         <h2>Select a sample</h2>
         <SampleObj name="example"
                    artist="artist"
                    src="example.wav"/>
         <SampleObj name="example2"
                    artist="artist2"
                    src="example.wav"/>
         <UploadObj/>
      </section>
   );
}