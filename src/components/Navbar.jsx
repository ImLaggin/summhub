import React from 'react'
import NavItems from './NavItems'

const Navbar = () => {
  return (
    <nav className='navbar flex flex-row bg-base-300 justify-between'>
      <button className="btn btn-lg rounded-full btn-ghost normal-case">SummHub</button>
      <ul className="menu menu-horizontal px-1">
        <NavItems text='Text Summarizer'/>
        <NavItems text='Audio Summarizer' classes='btn-disabled normal-case'/>
        <NavItems text='Video Summarizer' classes='btn-disabled normal-case'/>
      </ul>
    </nav>    
  )
}

export default Navbar