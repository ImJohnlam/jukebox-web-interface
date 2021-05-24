const axios = require('axios');

export const getFilters = async () => {
   try {
      const response = await axios.get('/filters');
      return response.data.filters
      
   } catch (e) {
      console.log(`err filter get e=${e}`);
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
         url: 'http://localhost:5000/upload',
         data: data,
         responseType: 'blob'
      });
      const mp3 = new Blob([response.data], { type: 'audio/wav' })
      const url = window.URL.createObjectURL(mp3)

      return url;
    } catch (e) {
      console.log('play audio error: ', e)
    }
}