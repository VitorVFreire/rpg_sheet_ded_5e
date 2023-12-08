import './Button.css'

const Button = (props) => {
    return (
        <button className='button-class' id={props.id} onClick={props.onClick}>
            {props.children}
        </button>
    )
}

export default Button