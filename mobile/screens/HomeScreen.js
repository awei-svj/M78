import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList, TouchableOpacity, StyleSheet } from 'react-native';

const BACKEND_URL = "http://localhost:8000";

export default function HomeScreen({ user, onLogout }) {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    // load demo product
    fetch(`${BACKEND_URL}/products/maotai-001`).then(r=>r.json()).then(p=>setProducts([p]));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>欢迎 {user.phone}</Text>
      <FlatList
        data={products}
        keyExtractor={i=>i.id}
        renderItem={({item}) => (
          <View style={styles.product}>
            <Text style={styles.productTitle}>{item.title}</Text>
            <Text>库存: {item.last_in_stock ? "有货" : "无货"}</Text>
            <Text>价格: {item.last_price}</Text>
            <View style={{flexDirection:'row', marginTop:8}}>
              <TouchableOpacity style={styles.btn} onPress={() => {
                fetch(`${BACKEND_URL}/subscribe`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user_id:user.id, product_id:item.id}) })
                  .then(()=>alert('已订阅（演示）'));
              }}>
                <Text style={styles.btnText}>订阅</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.btn, {marginLeft:8}]} onPress={()=>{
                fetch(`${BACKEND_URL}/refresh/${item.id}`, { method:'POST' }).then(()=> {
                  fetch(`${BACKEND_URL}/products/${item.id}`).then(r=>r.json()).then(p=>setProducts([p]));
                });
              }}>
                <Text style={styles.btnText}>手动刷新</Text>
              </TouchableOpacity>
            </View>
            <TouchableOpacity style={{marginTop:8}} onPress={()=>{
              // 在真实 App 中使用 deep link 打开官方商品页，示例仅弹窗说明
              alert('请使用官方 i茅台 App 或网页完成手动下单（示例）');
            }}>
              <Text style={{color:'#0066cc'}}>在官方客户端/网页手动下单</Text>
            </TouchableOpacity>
          </View>
        )}
      />
      <Button title="登出" onPress={onLogout} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex:1, padding:16 },
  title: { fontSize:18, marginBottom:12 },
  product: { padding:12, borderWidth:1, borderRadius:8, marginBottom:12 },
  productTitle: { fontWeight:'bold', marginBottom:6 },
  btn: { backgroundColor:'#007aff', paddingVertical:8, paddingHorizontal:12, borderRadius:6 },
  btnText: { color:'#fff' }
});
