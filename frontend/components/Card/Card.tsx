import { JSX } from "react";
import { CardProps } from "./Card.props";
import styles from "./Card.module.css";
import cn from "classnames"

export const Card = ({ children }: CardProps): JSX.Element => {
    return <div className={styles.card}>
        <div className={styles.first}>
            <div>
                <h2>Major</h2>
                <p>компания</p>
            </div>
             <div>
                <h2>12 дней</h2>
                <p>время</p>
            </div>
        </div>
        <div>
            <div>
                <h2>12000</h2>
                <p>цена</p>
            </div>
        </div>
    </div>;
};
