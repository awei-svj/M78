import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';

const BACKEND_URL = "http://localhost:8000"; // 在模拟器/设备上调整：Android emulator -> http://10.0.2.2:8000

export default function LoginScreen({ onLogin }) {
  const [phone, setPhone] = useState("");

  async function handleCreate() {
    if (!phone) return Alert.alert("请输入手机号");
    const resp = await fetch(`${BACKEND_URL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone }),
    });
    if (resp.ok) {
      const data = await resp.json();
      onLogin(data);
    } else {
      Alert.alert("创建用户失败");
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>i茅台 合规监测 Demo</Text>
      <TextInput placeholder="手机号（演示）" style={styles.input} value={phone} onChangeText={setPhone} keyboardType="phone-pad" />
      <Button title="创建用户并登录（演示）" onPress={handleCreate} />
      <Text style={styles.note}>注：真实场景请在官方客户端完成验证码登录，避免自动化登录。</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex:1, padding:20, justifyContent:'center' },
  title: { fontSize:20, marginBottom:12, textAlign:'center' },
  input: { borderWidth:1, marginBottom:12, padding:8, borderRadius:6 },
  note: { marginTop:12, fontSize:12, color:'#666' }
});
