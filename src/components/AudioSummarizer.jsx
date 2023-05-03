import {React, useState} from 'react'
import CopyToClipboard from 'react-copy-to-clipboard'

const AudioSummarizer = () => {

  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [type, setType] = useState("informative");
  const [disabled, setDisabled] = useState(true);

  const handleTypeChange = (e) => {
    setType(e.target.value)
  }

  const handleFileUpload = (e) => {
    setFile(e.target.files[0])
  }

  const handleSummarize = async () => {
    var formdata = new FormData();
    formdata.append("file", file);
    formdata.append("type", type);

    var requestOptions = {
      method: 'POST',
      body: formdata,
      redirect: 'follow'
    };

    fetch("http://localhost:5000/audio", requestOptions)
    .then(response => response.json())
    .then(data => {
      setText(data.text)
      setSummary(data.summary);
      setDisabled(false)
    })
    .catch(error => console.log('error', error));
  };

  return (
    <div className='mx-10 my-10'>
      <div className="flex justify-around">
        <div className="form-control">
          <div className="flex justify-between mb-5">
            <label className="label mb-5">
              <span className="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Transcribed Text</span>
            </label>
            <div className="flex flex-col">
              <div className="tooltip tooltip-right" data-tip="Select informative if single speaker, conversational if two speakers">
                <label className="label">
                  <span className="label-text">Summary Type</span>
                </label>
                <select className="select select-bordered border-accent" onChange={handleTypeChange}>
                  <option defaultChecked value="informative">Informative</option>
                  <option value="conversational">Conversational</option>
                </select>
              </div>
            </div>
          </div>
          <div className="bg-base-200 resize-none textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 mb-5 shadow-md shadow-accent !border-accent overflow-y-auto" disabled={disabled}>{text}</div>
          <div className="flex justify-between">
            <input type="file" className="file-input file-input-bordered file-input-accent w-full max-w-xs"  accept=".mp3,.aac,.wav" onChange={handleFileUpload}/>
            <button className="btn btn-accent" disabled={!file} onClick={handleSummarize}>Summarize</button>
          </div>
        </div>
        <div className="divider divider-horizontal"></div>
        <div className="form-control">
          <label className="label mb-10">
            <span className="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Generated Summary</span>
          </label>
          <div className="bg-base-200 textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 resize-none shadow-md shadow-accent mb-5 !border-accent overflow-y-auto" disabled={disabled} contentEditable={!disabled}>{summary}</div>
          <CopyToClipboard text={summary}>
            <button className="btn btn-block btn-accent" disabled={disabled}>Copy to Clipboard</button>
          </CopyToClipboard>
        </div>
      </div>
    </div>
  )
}

export default AudioSummarizer