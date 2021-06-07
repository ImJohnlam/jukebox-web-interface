import React, { useEffect, useState, useContext } from 'react';
import { Button, Card } from 'react-bootstrap';
import { GenerateContext } from '../GenerateContext';
import { getSampleInfo, getSample, getImage } from '../../api';
import './SampleSelect.css'

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

   const isSelected = () => getGenState('SAMPLE')['name'] === name;
   const select = () =>
      setGenState('SAMPLE', {
         name: name,
         file: new File([blob], info.src, {type:'audio/wav'})
      });

   return (
      <Card className="sample">
         <h3>{name} by {artist}</h3>
         <div className="test">
         {isSelected() ?
         <Button disabled={true}>Selected</Button>
         :
         <Button onClick={select}>Select</Button>
         }
         <Button onClick={e => window.open(url, '_blank')}>Play</Button>
         {imgStr ? <img className="spectrogram" src={imgStr}/> : ""}
         </div>
         
      </Card>
   )
}

const UploadObj = props => {
   const [getGenState, setGenState] = useContext(GenerateContext);

   const [blob, setBlob] = useState({});
   const [url, setURL] = useState("");
   const [imgStr, setImgStr] = useState("");

   let uploadInput;
   let name = null;

   const isSelected = () => getGenState('SAMPLE')['name'] === name;
   const select = async e => {
      e.preventDefault();
      const file = uploadInput.files[0];
      
      if (file) {
         name = file.name;
         setGenState('SAMPLE', {
            name: name,
            file: file
         });

         let fileToBlob = async (f) => new Blob([new Uint8Array(await f.arrayBuffer())], {type: f.type });
         let b = await fileToBlob(file);
         setBlob(b);
         setURL(window.URL.createObjectURL(b));
         getImage(b).then(base64 => setImgStr(base64));
      }
   }

   return (
      <Card className="sample">
         <h3>Upload a .wav file</h3>
         <form onSubmit={select}>
            <div>
               <input ref={ref => uploadInput = ref} type="file"/>
            </div>
            <div>
               {isSelected() ?
               <button disabled={true}>Selected</button>
               :
               <button>Select</button>
               }
               <Button onClick={e => window.open(url, '_blank')} disabled={url === ""}>Play</Button>
               {imgStr ? <img className="spectrogram" src={imgStr}/> : ""}
            </div>
         </form>
      </Card>

   );
}

export default function SampleSelect(props) {
   const [sampleInfo, setSampleInfo] = useState([]);

   useEffect(() => {
      getSampleInfo().then(info => setSampleInfo(info))
   }, [])

   return (
      <Card className="sample-selector">
         <h2>Select a sample</h2>
         {sampleInfo && sampleInfo.length ?
         sampleInfo.map(info => <SampleObj info={info}/>)
         : ""
         }
         <UploadObj/>
      </Card>
   );
}