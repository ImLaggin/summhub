import React, { useState } from 'react'

const Summarizer = () => {

  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [length, setLength] = useState("short") 

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const handleSummarize = async () => {
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
    .then(result => setSummary(JSON.parse(result)['summary']))
    .catch(error => console.log('error', error));
  };

  const handleLengthChange = (e) => {
    setLength(e.target.value)
  }

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
              <select className="select select-bordered" onChange={handleLengthChange}>
                <option defaultChecked value="short">Short</option>
                <option value="medium">Medium</option>
                <option value="long">Long</option>
                <option value="tweet">Tweet</option>
              </select>
            </div>
          </div>
          <textarea placeholder="Enter Input Text" className="bg-base-200 resize-none textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 mb-5 shadow-md shadow-accent" onChange={handleTextChange}></textarea>
          <div className="flex justify-between">
            <input type="file" className="file-input file-input-bordered w-full max-w-xs" />
            <button className="btn btn-accent" onClick={handleSummarize}>Summarize</button>
          </div>
        </div>
        <div className="divider divider-horizontal"></div>
        <div className="form-control">
          <label className="label mb-10">
            <span className="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Generated Summary</span>
          </label>
          <div className="bg-base-200 textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 resize-none shadow-md shadow-accent mb-5 !border-accent overflow-y-auto" contentEditable>{summary}</div>
          <button className="btn btn-block btn-accent">Copy to Clipboard</button>
        </div>
      </div>
    </div>
  )
}

export default Summarizer