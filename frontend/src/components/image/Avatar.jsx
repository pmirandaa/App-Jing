import styles from "./Avatar.module.css"

export default function Avatar(props) {
  return (
    <div className={styles.wrap}>
      <img src={props.src} className={styles.pic} />
    </div>
  )
}