import React, { useState, useEffect, useContext } from 'react';
import { Button, Accordion, Card } from 'react-bootstrap';
import './App.css';
import { SampleSelect, FilterSelect, Result } from './components/components'

function App() {
   return (
      <section className='container'>
         <div>
            <div>
               <h1>Welcome to Jukebox Web Interface</h1>
               <Button href="https://openai.com/blog/jukebox/">OpenAI Blog</Button>
            </div>
            
            
            <Accordion defaultActiveKey="0">
               <Card>
                  <Card.Header>
                     <Accordion.Toggle as={Button} eventKey="1">
                     Instructions
                     </Accordion.Toggle>
                  </Card.Header>
                  <Accordion.Collapse eventKey="1">
                     <Card.Body>
                        <div>1. Select a sample or upload your own .wav file</div>
                        <div>2. Apply a filter</div>
                        <div>3. Click generate</div>
                        <div>4. Click play result</div>
                     </Card.Body>
                  </Accordion.Collapse>
               </Card>
            </Accordion>
               
         </div>
         <SampleSelect/>
         <FilterSelect/>
         <Result/>
    </section>
  );
}

export default App;
