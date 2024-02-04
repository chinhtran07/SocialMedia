import { StyleSheet } from "react-native";

export default StyleSheet.create({
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
    }, avatar: {
        width: 80,
        height: 80,
        margin: 5
    }
});
