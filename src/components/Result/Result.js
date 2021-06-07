import React, { useEffect, useState, useContext } from 'react';
import { Button, Card } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext.js';
import { uploadFile, getImage } from '../../api';
import './Result.css'

export default function Result(props) {
   const [genState, _] = useContext(GenerateContext);
   const [blob, setBlob] = useState({});
   const [url, setURL] = useState("");
   const [imgStr, setImgStr] = useState("");

   const generate = async e => {
      uploadFile(genState('SAMPLE')['file'], genState('FILTERS')).then(b => {
         console.log(`b is ${b}`)
         setBlob(b);
         setURL(window.URL.createObjectURL(b));
         getImage(b).then(base64 => setImgStr(base64));
      })   
   }

   return (
      <div>
         <Card className='result-selector'>
            <h2>Result Audio</h2>
            <Button onClick={generate} disabled={genState('SAMPLE') === ""}>Generate</Button>
            <Button onClick={e => window.open(url, '_blank')} disabled={url === ""}>Play Result</Button>
            {imgStr ? <img className='spectrogram' src={imgStr}/> : ""}
         </Card>
         
      </div>
   );
}