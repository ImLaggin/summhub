import React from 'react'

const Summarizer = () => {
  return (
    <div className='mx-10 my-10'>
      <div className="flex justify-around">
        <div className="form-control">
          <div className="flex justify-between mb-5">
            <label class="label mb-5">
              <span class="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Input Text</span>
            </label>
            <div className="flex flex-col">
              <label className="label">
                <span className="label-text">Summary Length</span>
              </label>
              <select className="select select-bordered">
                <option selected>Short</option>
                <option>Medium</option>
                <option>Long</option>
                <option>Tweet</option>
              </select>
            </div>
          </div>
          <textarea placeholder="Enter Input Text" className="bg-base-200 resize-none textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 mb-5 shadow-md shadow-accent" ></textarea>
          <div className="flex justify-between">
            <input type="file" className="file-input file-input-bordered w-full max-w-xs" />
            <button className="btn btn-accent">Submit</button>
          </div>
        </div>
        <div className="divider divider-horizontal"></div>
        <div className="form-control">
          <label class="label mb-10">
            <span class="label-text text-lg btn btn-active normal-case no-animation pointer-events-none">Generated Summary</span>
          </label>
          <textarea className="bg-base-200 textarea textarea-bordered textarea-accent textarea-lg w-[512px] h-80 resize-none shadow-md shadow-accent mb-5 !border-accent pointer-events-none" disabled></textarea>
          <button className="btn btn-block btn-accent">Copy to Clipboard</button>
        </div>
      </div>
    </div>
  )
}

export default Summarizer