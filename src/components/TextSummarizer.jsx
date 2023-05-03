import React, { useState } from 'react'
import { CopyToClipboard } from 'react-copy-to-clipboard';

const Summarizer = () => {

  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [length, setLength] = useState("short");
  const [disabled, setDisabled] = useState(true);

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const handleLengthChange = (e) => {
    setLength(e.target.value)
  }

  const handleFileUpload = (e) => {
    setFile(e.target.files[0])
  }

  const handleSummarize = async () => {
    if (text !== '') {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");
      const raw = JSON.stringify({
        "text": text,
        "length": length
      });

      const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
      };

      fetch("http://localhost:5000", requestOptions)
      .then(response => response.text())
      .then(result => {
        setSummary(JSON.parse(result)['summary']);
        setDisabled(false);
      })
      .catch(error => console.log('error', error));
    } else {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('length', length);

      fetch('http://localhost:5000/file', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        setSummary(data.summary);
        setDisabled(false)
      })
      .catch(error => console.error(error));
    }
  };

  return (
    <div className='mx-10 my-10'>
      <div className="flex justify-around">
        <div className="form-control">
          <div className="flex justify-between mb-5">
            <label className="label mb-5">
              <span className="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Input Text</span>
            </label>
            <div className="flex flex-col">
              <label className="label">
                <span className="label-text">Summary Length</span>
              </label>
              <select className="select select-bordered border-accent" onChange={handleLengthChange}>
                  <option defaultChecked value="short">Short</option>
                  <option value="medium">Medium</option>
                  <option value="long">Long</option>
                  <option value="tweet">Tweet</option>
                </select>
            </div>
          </div>
          <textarea placeholder="Enter Input Text" className="bg-base-200 resize-none textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 mb-5 shadow-md shadow-accent !border-accent" disabled={file} onChange={handleTextChange}></textarea>
          <div className="flex justify-between">
            <input type="file" className="file-input file-input-bordered file-input-accent w-full max-w-xs" onChange={handleFileUpload} disabled={text} accept=".pdf,.doc,.docx,.txt"/>
            <button className="btn btn-accent" onClick={handleSummarize} disabled={!text && !file}>Summarize</button>
          </div>
        </div>
        <div className="divider divider-horizontal"></div>
        <div className="form-control">
          <label className="label mb-10">
            <span className="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Generated Summary</span>
          </label>
          <div className="bg-base-200 textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 resize-none shadow-md shadow-accent mb-5 !border-accent overflow-y-auto" contentEditable={!disabled} disabled={disabled}>{summary}</div>
          <CopyToClipboard text={summary}>
            <button className="btn btn-block btn-accent" disabled={disabled}>Copy to Clipboard</button>
          </CopyToClipboard>
        </div>
      </div>
    </div>
  )
}

export default Summarizer