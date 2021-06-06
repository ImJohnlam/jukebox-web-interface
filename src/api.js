const axios = require('axios');

export const getFilters = async () => {
   try {
      const response = await axios.get('/filters');
      return response.data.filters
      
   } catch (e) {
      console.log(`err filter get e=${e}`);
   }
}

export const getSampleInfo = async () => {
   try {
      const response = await axios.get('/sample_info');
      console.log(response.data)
      return response.data.samples
   } catch (e) {
      console.log(`err sample info get e=${e}`)
   }
}

export const getSample = async src => {
   try {
      const response = await axios({
         method: 'get',
         url: `/sample/${src}`,
         responseType: 'blob'
      })
      // const response = axios(`/sample/${src}`);
      const blob = new Blob([response.data], { type: 'audio/wav' });
      // const url = window.URL.createObjectURL(mp3);
      return blob;
   } catch (e) {
      console.log(`err sample get e=${e}`)
   }
}

export const uploadFile = async (file, filters) => {
   const data = new FormData();

   data.append('file', file);

   // TODO, filters param here
   data.append('filters', JSON.stringify(filters));

   console.log('uploading file:', file)
   

   try {
      const response = await axios({
         method: 'post',
         url: '/upload',
         data: data,
         responseType: 'blob'
      });
      const blob = new Blob([response.data], { type: 'audio/wav' })
      // const url = window.URL.createObjectURL(mp3)

      return blob;
    } catch (e) {
      console.log('play audio error: ', e)
    }
}

export const getImage = async audioBlob => {
   const data = new FormData();
   console.log(`audioblob=${audioBlob}`)
   const file = new File([audioBlob], "test.wav", {type:'audio/wav'})


   data.append('file', file);

   try {
      const response = await axios({
         method: 'post',
         url: '/get_image',
         data: data,
         responseType: 'arraybuffer'
      });
      const base64 = btoa(new Uint8Array(response.data).reduce(
         (data, byte) => data + String.fromCharCode(byte), '',),);
      
      return "data:;base64," + base64;
   } catch (e) {
      console.log(`getimage err e=${e}`)
   }
}