import { useContext, useEffect, useState } from "react";
import { Image, StyleSheet, TextInput, View, TouchableOpacity, Text } from "react-native"
import DropDownPicker from "react-native-dropdown-picker";
import MyContext from "../../configs/MyContext";
import API, { authApi, endpoints } from "../../configs/API";
import AsyncStorage from '@react-native-async-storage/async-storage'

const Login = ({ navigation }) => {
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [roles, setRoles] = useState([
        { label: 'Cuu Sinh Vien', value: 1 },
        { label: 'Giang Vien', value: 2 },
        { label: 'Quan tri vien', value: 3 },
    ]);
    const [open, setOpen] = useState(false);
    const [value, setValue] = useState(null);

    const [loading, setLoading] = useState(false);
    const [user, dispatch] = useContext(MyContext);


    const login = async () => {
        setLoading(true)
 
        try {
            let res = await API.post(endpoints['login'], {
                "username": username,
                "password": password,
                "role": value
            }, {
                headers: { 'Content-Type': 'application/json' }
            });

            await AsyncStorage.setItem("access-token", res.data.access_token)
            let user = await authApi(res.data.access_token).get(endpoints['current-user']);
            dispatch({
                type: "login",
                payload: user.data
            });
            navigation.navigate("Home");
        } catch (ex) {
            console.error(ex)
        } finally {
            setLoading(false)
        }
    }

    return (
        <View style={styles.container}>
            <Image source={require("../../assets/oulogo.png")} style={{ width: 400, height: 300 }} />
            <DropDownPicker
                style={{ marginBottom: 10 }}
                dropDownStyle={styles.dropdownDropStyle}
                open={open}
                value={value}
                items={roles}
                setOpen={setOpen}
                setValue={setValue}
                setItems={setRoles}
                onChangeItem={(role) => setValue(role.value)}
            />
            <TextInput style={styles.input}
                placeholder="Username"
                value={username}
                onChangeText={(text) => setUsername(text)}
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                secureTextEntry={true}
                value={password}
                onChangeText={(text) => setPassword(text)}
            />
            <TouchableOpacity style={styles.button} onPress={login}>
                <Text style={styles.buttonText}>Login</Text>
            </TouchableOpacity>
            <View style={{flexDirection: "row"}}>
                <TouchableOpacity onPress={() => {navigation.navigate("Register")}}>
                    <Text> New account</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({

    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 16,
    },
    dropdownDropStyle: {
        backgroundColor: 'gray',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 16,
    },
    input: {
        width: '100%',
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        borderRadius: 8,
        marginBottom: 16,
        paddingLeft: 8,
    },
    button: {
        backgroundColor: 'blue',
        padding: 10,
        borderRadius: 8,
    },
    buttonText: {
        color: 'white',
        textAlign: 'center',
    },
});

export default Login 