// paxmeet-icons React component — generated.
// Usage:  import { PaxmeetIcon } from "@/components/paxmeet-icons/PaxmeetIcon";
//         <PaxmeetIcon name="home" size={24} color="#7332D6" />
import "./paxmeet-icons.css";

export function PaxmeetIcon({ name, size = 24, color, className = "", style, ...rest }) {
  return (
    <i
      className={`pmi pmi-${name} ${className}`}
      style={{ fontSize: size, color, ...style }}
      aria-hidden="true"
      {...rest}
    />
  );
}
