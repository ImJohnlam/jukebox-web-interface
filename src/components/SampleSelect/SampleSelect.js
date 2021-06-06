import React, { useEffect, useState, useContext } from 'react';
import { Button } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext';
import { getSampleInfo, getSample, getImage } from '../../api';

const SampleObj = props => {
   const [getGenState, setGenState] = useContext(GenerateContext);
   const [blob, setBlob] = useState({});
   const [url, setURL] = useState("");
   const [imgStr, setImgStr] = useState("");

   const info = props.info;
   const name = info.name;
   const artist = info.artist;

   useEffect(() => {
      getSample(info.src).then(b => {
         setBlob(b);
         setURL(window.URL.createObjectURL(b));
         getImage(b).then(base64 => setImgStr(base64))
      });
   }, []);

   const isSelected = () => getGenState('SAMPLE') == name;
   const select = () => setGenState('SAMPLE', new File([blob], info.src, {type:'audio/wav'}));

   return (
      <div>
         <b>{name} by {artist}</b>
         {isSelected() ?
         <Button disabled={true}>Selected</Button>
         :
         <Button onClick={select}>Select</Button>
         }
         <Button onClick={e => window.open(url, '_blank')}>Play</Button>
         {imgStr ? <img src={imgStr}/> : ""}
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
   );
}

export default function SampleSelect(props) {
   const [sampleInfo, setSampleInfo] = useState([]);

   useEffect(() => {
      getSampleInfo().then(info => setSampleInfo(info))
   }, [])

   return (
      <section className='container'>
         <h2>Select a sample</h2>
         {sampleInfo && sampleInfo.length ?
         sampleInfo.map(info => <SampleObj info={info}/>)
         : ""
         }
         <UploadObj/>
      </section>
   );
}