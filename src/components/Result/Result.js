import React, { useEffect, useState, useContext } from 'react';
import { Button } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext.js';
import { uploadFile, getImage } from '../../api';

export default function Result(props) {
   const [genState, _] = useContext(GenerateContext);
   const [blob, setBlob] = useState({});
   const [url, setURL] = useState("");
   const [imgStr, setImgStr] = useState("");

   // useEffect(() => {
   //    getSample(info.src).then(b => {
   //       setBlob(b);
   //       setURL(window.URL.createObjectURL(b));
   //       getImage(b).then(base64 => setImgStr(base64))
   //    });
   // }, []);

   const generate = async e => {
      uploadFile(genState('SAMPLE'), genState('FILTERS')).then(b => {
         console.log(`b is ${b}`)
         setBlob(b);
         setURL(window.URL.createObjectURL(b));
         getImage(b).then(base64 => setImgStr(base64));
      })   
   }

   return (
      <div>
         <Button onClick={generate} disabled={genState('SAMPLE') === ""}>Generate</Button>
         <Button onClick={e => window.open(url, '_blank')} disabled={url === ""}>Play</Button>
         {imgStr ? <img src={imgStr}/> : ""}
      </div>
   );
}