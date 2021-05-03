import React, { useEffect, useState, useContext } from 'react';
import { Button } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext';

const SampleObj = (props) => {
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
         
      </section>
   );
}