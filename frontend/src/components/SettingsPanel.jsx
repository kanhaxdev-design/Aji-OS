import React, { useEffect, useState } from 'react'
import { Settings as SettingsIcon, Zap, Volume2, Eye } from 'lucide-react'
import { useStore } from '../store/appStore'
import { systemService } from '../services/api'

function SettingsPanel() {
  const {
    currentProvider,
    setCurrentProvider,
    temperature,
    updateTemperature,
    maxTokens,
    updateMaxTokens,
    voiceEnabled,
    toggleVoice,
    pluginsEnabled,
    togglePlugins,
  } = useStore()

  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProviders()
  }, [])

  const loadProviders = async () => {
    try {
      const data = await systemService.getProviders()
      setProviders(data.providers || [])
      setLoading(false)
    } catch (error) {
      console.error('Failed to load providers:', error)
    }
  }

  const handleProviderChange = async (provider) => {
    try {
      await systemService.switchProvider(provider)
      setCurrentProvider(provider)
    } catch (error) {
      console.error('Failed to switch provider:', error)
    }
  }

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-12">
      <div className="max-w-2xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <SettingsIcon size={28} className="text-aji-accent" />
            <h1 className="text-3xl font-bold">Settings</h1>
          </div>
          <p className="text-gray-400">Configure Aji OS preferences</p>
        </div>

        {/* AI Provider Section */}
        <div className="glass rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Zap size={20} className="text-aji-accent" />
            AI Provider
          </h2>
          <div className="space-y-3">
            {loading ? (
              <p className="text-gray-400">Loading providers...</p>
            ) : (
              providers.map((provider) => (
                <label key={provider} className="flex items-center gap-3 cursor-pointer group">
                  <input
                    type="radio"
                    name="provider"
                    value={provider}
                    checked={currentProvider === provider}
                    onChange={(e) => handleProviderChange(e.target.value)}
                    className="w-4 h-4 accent-aji-accent"
                  />
                  <span className="group-hover:text-aji-accent transition capitalize">
                    {provider}
                  </span>
                </label>
              ))
            )}
          </div>
        </div>

        {/* Model Settings */}
        <div className="glass rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold mb-4">Model Parameters</h3>

          {/* Temperature */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Temperature: {temperature.toFixed(2)}
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={temperature}
              onChange={(e) => updateTemperature(parseFloat(e.target.value))}
              className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-aji-accent"
            />
            <p className="text-xs text-gray-400 mt-1">
              Lower = more focused, Higher = more creative
            </p>
          </div>

          {/* Max Tokens */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Max Tokens: {maxTokens}
            </label>
            <input
              type="range"
              min="256"
              max="4096"
              step="256"
              value={maxTokens}
              onChange={(e) => updateMaxTokens(parseInt(e.target.value))}
              className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-aji-accent"
            />
            <p className="text-xs text-gray-400 mt-1">
              Controls the maximum length of responses
            </p>
          </div>
        </div>

        {/* Features Section */}
        <div className="glass rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Features</h3>
          <div className="space-y-3">
            <label className="flex items-center justify-between cursor-pointer group">
              <span className="flex items-center gap-2 group-hover:text-aji-accent transition">
                <Volume2 size={18} className="text-aji-accent" />
                Voice Input/Output
              </span>
              <input
                type="checkbox"
                checked={voiceEnabled}
                onChange={toggleVoice}
                className="w-4 h-4 accent-aji-accent cursor-pointer"
              />
            </label>
            <label className="flex items-center justify-between cursor-pointer group">
              <span className="flex items-center gap-2 group-hover:text-aji-accent transition">
                <Eye size={18} className="text-aji-accent" />
                System Plugins
              </span>
              <input
                type="checkbox"
                checked={pluginsEnabled}
                onChange={togglePlugins}
                className="w-4 h-4 accent-aji-accent cursor-pointer"
              />
            </label>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 p-4 glass rounded-lg text-center text-sm text-gray-400">
          <p>Aji OS v1.0 • Built with React + FastAPI</p>
          <p className="mt-1">© 2026 Aji OS. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}

export default SettingsPanel
