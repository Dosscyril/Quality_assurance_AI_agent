import { motion } from "framer-motion";

export default function Landing({ onStart }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white flex flex-col items-center justify-center px-6">

      <motion.h1
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-5xl font-bold mb-6 text-center"
      >
        🚀 AI QA Agent
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-lg text-gray-300 max-w-xl text-center mb-8"
      >
        <span className="text-blue-400">AI-powered</span> website testing platform.
        Detect UI issues, broken links, and generate intelligent QA reports.
      </motion.p>

      <motion.button
        whileHover={{ scale: 1.1 }}
        onClick={onStart}
        className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg text-lg shadow-lg shadow-blue-500/30"
      >
        Try it now →
      </motion.button>
    </div>
  );
}