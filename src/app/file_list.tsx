import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface File {
  name: string;
  size: number;
  path: string;
}

const file_list: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/files/')
      .then(response => {
        setFiles(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the files!', error);
      });
  }, []);

  return (
    <div>
      <h1>Files</h1>
      <ul>
        {files.map(file => (
          <li key={file.path}>
            <strong>{file.name}</strong> (Size: {file.size} bytes)
          </li>
        ))}
      </ul>
    </div>
  );
};

export default file_list