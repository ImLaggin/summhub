import React from 'react'
import { NavLink } from 'react-router-dom'

const Navbar = () => {

  const activeButton = 'btn-active btn btn-ghost normal-case mr-2'
  const normalButton = 'btn btn-ghost normal-case mr-2'

  return (
    <nav className='navbar flex flex-row bg-base-300 justify-between'>
      <button className="btn btn-lg rounded-full btn-ghost normal-case ml-10">SummHub</button>
      <ul className="menu menu-horizontal mr-16">
        <NavLink to='/' className={({isActive}) => (isActive ? activeButton : normalButton)}><button >Text Summarizer</button></NavLink>
        <NavLink to='/audio' className={({isActive}) => (isActive ? activeButton : normalButton)}><button >Audio Summarizer</button></NavLink>
        <NavLink><button className='btn btn-disabled btn-ghost normal-case mr-2'>Video Summarizer</button></NavLink>
      </ul>
    </nav>    
  )
}

export default Navbar