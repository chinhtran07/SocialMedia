import { StyleSheet } from "react-native"

export default StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    image: {
        width: 400,
        height: 300,
        marginBottom: 20,
    },
    dropbox: {
        height: 30,
        width: 300,
        alignSelf: "center",
        marginBottom: 30,
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomWidth: 1,
        borderColor: '#555',
        marginBottom: 10,
        paddingHorizontal: 10,
    },
    icon: {
        marginRight: 10,
    },
    input: {
        flex: 1,
        height: 40,
        fontSize: 16,
        color: '#555',
        // Add other input styles as needed
    },
    button: {
        backgroundColor: 'gray',
        borderRadius: 20,
        paddingHorizontal: 20,
        paddingVertical: 10,
        marginBottom: 10,
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
    },
    forgotPassword: {
        marginTop: 10,
    },
    forgotPasswordText: {
        color: 'blue',
        fontSize: 16,
    },
});