import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import TextSummarizer from "./components/TextSummarizer";
import { Routes, Route } from "react-router-dom";
import AudioSummarizer from "./components/AudioSummarizer";

export default function App() {
  return (
    <>
      <Navbar/>
        <Routes>
          <Route path="/" element={<TextSummarizer />} />
          <Route path="/audio" element={<AudioSummarizer />}/>
        </Routes>
      <Footer/>
    </>
  )
}
