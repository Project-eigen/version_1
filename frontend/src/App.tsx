import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import AuthGate from './pages/AuthGate'
import AuthSuccess from './pages/AuthSuccess'
import FamilySettings from './pages/FamilySettings'
import Cabinet from './pages/Cabinet'
import Scanner from './pages/Scanner'
import ScanApproval from './pages/ScanApproval'
import FamilyInbox from './pages/FamilyInbox'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) {
    return (
      <div className="loading-overlay" style={{ height: '100dvh' }}>
        <div className="loading-spinner" />
      </div>
    )
  }
  if (!user) return <Navigate to="/" replace />
  return <>{children}</>
}

function AppRoutes() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading-overlay" style={{ height: '100dvh' }}>
        <div className="loading-spinner" />
      </div>
    )
  }

  return (
    <div className="app-shell">
      <Routes>
        {/* Public */}
        <Route path="/" element={user ? <Navigate to="/home" replace /> : <AuthGate />} />
        <Route path="/auth/success" element={<AuthSuccess />} />

        {/* Protected */}
        <Route path="/home" element={<ProtectedRoute><FamilySettings /></ProtectedRoute>} />
        <Route path="/cabinet" element={<ProtectedRoute><Cabinet /></ProtectedRoute>} />
        <Route path="/scan" element={<ProtectedRoute><Scanner /></ProtectedRoute>} />
        <Route path="/scan/approve" element={<ProtectedRoute><ScanApproval /></ProtectedRoute>} />
        <Route path="/inbox" element={<ProtectedRoute><FamilyInbox /></ProtectedRoute>} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}
