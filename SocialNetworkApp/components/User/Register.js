import { useState } from "react"
import API, { endpoints } from "../../configs/API"
import * as ImagePicker from 'expo-image-picker';
import { TextInput, TouchableOpacity, View, Image, ActivityIndicator, Text } from "react-native";
import MyStyles from "../../styles/MyStyles";


const Register = ({ navigation }) => {
    const [user, setUser] = useState({
        "first_name": "",
        "last_name": "",
        "username": "",
        "password": "",
        "email": "",
        "student_id": "",
        "avatar": ""
    })

    const [loading, setLoading] = useState(false)

    const register = async () => {
        setLoading(true);

        const form = new FormData();

        for (let key in user)
            if (key === 'avatar') {
                form.append(key, {
                    uri: user[key].uri,
                    name: user[key].fileName,
                    type: user[key].type
                })
            } else {
                form.append(key, user[key]);
            }

        try {
            let res = await API.post(endpoints['register'], form, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.info(res.data);
            navigation.navigate("Login");
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }
    const picker = async () => {
        let { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            alert("Permission Denied!");
        } else {
            let res = await ImagePicker.launchImageLibraryAsync();
            if (!res.canceled) {
                change("avatar", res.assets[0])
            }
        }
    }
    const change = (field, value) => {
        setUser(current => {
            return { ...current, [field]: value }
        })
    }

    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.title}>ĐĂNG KÝ</Text>

            <TextInput value={user.first_name} onChangeText={t => change("first_name", t)} style={MyStyles.input} placeholder="Tên..." />
            <TextInput value={user.last_name} onChangeText={t => change("last_name", t)}  style={MyStyles.input} placeholder="Họ và tên lót..." />
            <TextInput value={user.username} onChangeText={t => change("username", t)}  style={MyStyles.input} placeholder="Tên đăng nhập..." />
            <TextInput value={user.password} onChangeText={t => change("password", t)} secureTextEntry style={MyStyles.input} placeholder="Mật khẩu..." />
            <TextInput value={user.email} onChangeText={t => change("email", t)}  style={MyStyles.input} placeholder="Email..." />
            <TextInput value={user.student_id} onChangeText={t => change("student_id", t)}  style={MyStyles.input} placeholder="Ma so sinh vien..." />

            <TextInput style={MyStyles.input} secureTextEntry placeholder="Xác nhận mật khẩu..." />
            <TouchableOpacity style={MyStyles.input} onPress={picker}>
                <Text>Chọn ảnh đại diện...</Text>
            </TouchableOpacity>

            {user.avatar?<Image style={MyStyles.avatar} source={{uri: user.avatar.uri}} />:""}

            {loading===true?<ActivityIndicator />:<>
                <TouchableOpacity onPress={register}>
                    <Text style={MyStyles.button}>Đăng ký</Text>
                </TouchableOpacity>
            </>}
            
        </View>
    );
}

export default Register