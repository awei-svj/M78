import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import { useState } from 'react';

export default function App() {
  const [user, setUser] = useState(null);

  if (!user) {
    return <LoginScreen onLogin={setUser} />;
  }
  return <HomeScreen user={user} onLogout={() => setUser(null)} />;
}
