import { Text, TextInput, TouchableOpacity, View, Image } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import MyContext from "../../configs/MyContext";
import MyStyles from "../../styles/MyStyles"
import API, { authApi, endpoints } from "../../configs/API"
import Style from "./Style"
import { useEffect, useState } from "react";
import DropDownPicker from "react-native-dropdown-picker";
// import { Icon } from "react-native-vector-icons/icon";

const Login = ({ navigation }) => {
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [loading, setLoading] = useState(false);

    const [open, setOpen] = useState(false);
    const [value, setValue] = useState(null);
    const [roles, setRoles] = useState([
        { label: 'Cựu sinh viên', value: 1 },
        { label: 'Giảng viên', value: 2 },
        { label: 'Quản trị viên', value: 3 }
    ]);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const fetchedRoles = await fetchRoles();
                setRoles(fetchedRoles);
            } catch (error) {
                console.error('Error fetching roles:', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        // Set the default value when roles are updated
        if (roles.length > 0 && value === null) {
            setValue(roles[0].value);
        }
    }, [roles, value]);
    const fetchRoles = async () => {
        return [
            { label: 'Cựu sinh viên', value: 1 },
            { label: 'Giảng viên', value: 2 },
            { label: 'Quản trị viên', value: 3 }
        ]
    };
    const login = async () => {
        setLoading(true);

        try {
            let res = await API.post(endpoints['login'], {
                "username": username,
                "password": password,
                "role": value
            });

            await AsyncStorage.setItem("access-token", res.data.access_token)
            let user = await authApi(res.data.access_token).get(endpoints['current-user']);
            dispatch({
                type: "login",
                payload: user.data
            });
            navigation.navigate("Home");
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    const register = () => {
        navigation.navigate("Register")
    }

    return (
        <View style={MyStyles.container}>
            <Image source={require('../../assests/oulogo.png')} style={Style.image} />
            <DropDownPicker
                style={Style.dropbox}
                open={open}
                value={value}
                items={roles.map(role => ({ label: role.label, value: role.value }))}
                setOpen={setOpen}
                setValue={setValue}
                setRoles={setRoles}
            />
            <View style={Style.inputContainer}>
                {/* <Icon name="user" size={20} color="#555" style={Style.icon}/> */}
                <TextInput
                    style={Style.input}
                    placeholder="Username"
                    value={username}
                    onChangeText={(text) => setUsername(text)}
                />
            </View>
            <View style={Style.inputContainer}>
                <TextInput
                    style={Style.input}
                    placeholder="Password"
                    secureTextEntry
                    value={password}
                    onChangeText={(text) => setPassword(text)}
                />
            </View>
            <TouchableOpacity style={Style.button} onPress={login}>
                <Text style={Style.buttonText}>Đăng nhập</Text>
            </TouchableOpacity>
            <View>
                <TouchableOpacity>
                    <Text style={Style.forgotPassword}>Quên mật khẩu?</Text>
                </TouchableOpacity>
                <TouchableOpacity>
                    <Text style={Style.forgotPassword} onPress={register}>Tạo tài khoản</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

export default Login;

