import './Button.css'

const Button = (props) => {
    return (
        <button className='button-class'>
            {props.children}
        </button>
    )
}

export default Button